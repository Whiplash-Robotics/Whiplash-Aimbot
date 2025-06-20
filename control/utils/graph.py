import argparse
import os

import matplotlib
import matplotlib.pyplot as plt

# --- Matplotlib Font Configuration ---
# Attempt to set a font that supports emojis.
# This should be done before any plotting.
# You might need to install 'Noto Color Emoji' or ensure one of these is available.
try:
    # Prioritize Noto Color Emoji as it's a comprehensive emoji font
    # and often works well across platforms when installed.
    font_prefs = ["Noto Color Emoji", "Segoe UI Emoji", "Apple Color Emoji"]
    available_fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]

    chosen_font = None
    for font_name in font_prefs:
        if font_name in available_fonts:
            chosen_font = font_name
            break

    if chosen_font:
        plt.rcParams["font.family"] = chosen_font
        # If you still have issues, you might need to specify sans-serif
        # and add your emoji font to the sans-serif list:
        # plt.rcParams['font.sans-serif'] = [chosen_font] + plt.rcParams['font.sans-serif']
        # plt.rcParams['font.family'] = 'sans-serif'
        print(f"💡 Matplotlib using font: {chosen_font} for emojis.")
    else:
        print("⚠️ Warning: Could not find 'Noto Color Emoji', 'Segoe UI Emoji', or 'Apple Color Emoji'. Emojis in plots might not render correctly. 💡 Consider installing 'Noto Color Emoji' for best results.")

except Exception as e:
    print(f"⚠️ Warning: Could not configure matplotlib font settings: {e}")
# --- End Matplotlib Font Configuration ---


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Graphs RPM over time from sensor log files and saves them as images. Also logs RPM values."
    )
    parser.add_argument(
        "--input_path",
        "-i",
        default="../outputs/raw",
        help="Path to the input log file or directory containing log files (default: ../outputs/raw)",
    )
    parser.add_argument(
        "--output_folder",
        "-o",
        default="../outputs/graph",
        help="Path to the folder where output graphs and RPM logs will be saved (default: ../outputs/graph)",
    )
    parser.add_argument(
        "--angular_resolution_segments",
        "-a",
        type=int,
        default=30,
        help="Number of segments the 360-degree rotation is divided into by the sensor (default: 30). Each switch signifies rotation by 360/angular_resolution_segments degrees.",
    )
    parser.add_argument(
        "--start_time",
        "-st",
        type=float,
        default=None,
        help="Optional start time (in seconds) for the x-axis of the graph to zoom in.",
    )
    parser.add_argument(
        "--end_time",
        "-et",
        type=float,
        default=None,
        help="Optional end time (in seconds) for the x-axis of the graph to zoom in.",
    )
    return parser.parse_args()


def process_log_file(filepath, angular_resolution_segments):
    """
    Reads a single log file, processes sensor data, and calculates timestamps, RPMs, and source line numbers.
    """
    timestamps_s = []
    rpms = []
    source_line_numbers = []
    current_total_time_s = 0.0
    logging_active = False
    processed_data_for_this_file = False

    try:
        with open(filepath, "r") as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line == "LOGGING_START":
                    if logging_active and processed_data_for_this_file:
                        print(f"⚠️ Warning: File '{os.path.basename(filepath)}' contains multiple LOGGING_START sections. Only the first will be processed.")
                        break
                    logging_active = True
                    current_total_time_s = 0.0
                    timestamps_s = []
                    rpms = []
                    source_line_numbers = []
                    processed_data_for_this_file = False
                    continue

                if line == "LOGGING_STOP":
                    if not logging_active:
                        continue
                    logging_active = False
                    break

                if logging_active:
                    if ":" in line and (
                        line.startswith("ON_ms:") or line.startswith("OFF_ms:")
                    ):
                        try:
                            _, value_str = line.split(":", 1)
                            event_duration_ms = float(value_str)

                            if event_duration_ms <= 0:
                                print(f"⚠️ Warning: Non-positive duration ({event_duration_ms}ms) in '{os.path.basename(filepath)}' on line {line_number}: '{line}'. Skipping.")
                                continue

                            rpm = 60000.0 / (
                                angular_resolution_segments * event_duration_ms
                            )

                            if rpm < 0 or rpm > 10000:  # Basic sanity check for RPM
                                print(f"⚠️ Warning: Unreasonable RPM value ({rpm}) in '{os.path.basename(filepath)}' on line {line_number}: '{line}'. Skipping.")
                                continue
                            event_duration_s = event_duration_ms / 1000.0
                            current_total_time_s += event_duration_s

                            timestamps_s.append(current_total_time_s)
                            rpms.append(rpm)
                            source_line_numbers.append(line_number)
                            processed_data_for_this_file = True

                        except ValueError:
                            print(f"⚠️ Warning: Could not parse data value in '{os.path.basename(filepath)}' on line {line_number}: '{line}'. Skipping.")
                        except ZeroDivisionError:
                            print(f"🛑 Critical Warning: Zero division error for '{os.path.basename(filepath)}' line {line_number}: '{line}'. This should not happen if angular_resolution_segments is positive.")

    except FileNotFoundError:
        print(f"🛑 Error: Input file '{filepath}' not found during processing.")
        return None, None, None
    except Exception as e:
        print(f"🛑 An unexpected error occurred while processing file '{filepath}': {e}")
        return None, None, None

    if not timestamps_s and not processed_data_for_this_file:
        return None, None, None

    return timestamps_s, rpms, source_line_numbers


def plot_and_save_rpm(
    timestamps_s,
    rpms,
    angular_resolution_segments,
    input_filepath,
    output_filepath,
    start_time=None,
    end_time=None,
):
    """
    Plots RPM over time and saves the graph to a file.
    Allows specifying start and end times for x-axis zoom.
    """
    if not timestamps_s or not rpms:
        print(f"🛑 No data provided to plot for {os.path.basename(input_filepath)}. Plotting skipped.")
        return

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(timestamps_s, rpms, marker="o", linestyle="-", markersize=4, linewidth=1.5)

    ax.set_xlabel("Time (s) ⏰")
    ax.set_ylabel("RPM (Revolutions Per Minute) ⚙️")

    degrees_per_segment = 360.0 / angular_resolution_segments
    title_str = (
        f"Motor RPM Over Time 📈\n"
        f"Source: {os.path.basename(input_filepath)}\n"
        f"(Angular Segments: {angular_resolution_segments}, Degrees/Segment: {degrees_per_segment:.2f}°)"
    )

    zoom_applied_info = []
    if start_time is not None:
        zoom_applied_info.append(f"Start: {start_time:.2f}s")
    if end_time is not None:
        zoom_applied_info.append(f"End: {end_time:.2f}s")

    if zoom_applied_info:
        title_str += f"\nZoom: [{', '.join(zoom_applied_info)}]"

    ax.set_title(title_str)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)

    if start_time is not None and end_time is not None:
        ax.set_xlim(start_time, end_time)
    elif start_time is not None:
        ax.set_xlim(left=start_time)
    elif end_time is not None:
        ax.set_xlim(right=end_time)

    if len(timestamps_s) > 0:
        avg_rpm = sum(rpms) / len(rpms)
        max_rpm = max(rpms)
        min_rpm = min(rpms)
        ax.text(
            0.01,
            0.01,
            f"Overall Avg RPM: {avg_rpm:.2f}\nOverall Max RPM: {max_rpm:.2f}\nOverall Min RPM: {min_rpm:.2f}",
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment="bottom",
            bbox=dict(boxstyle="round,pad=0.3", fc="wheat", alpha=0.5),
        )

    plt.tight_layout()
    try:
        plt.savefig(output_filepath)
    except Exception as e:
        print(f"🛑 Error saving plot to '{output_filepath}': {e}")
    finally:
        plt.close(fig)


def main():
    """Main function to orchestrate the script."""
    args = parse_arguments()

    if args.angular_resolution_segments <= 0:
        print(f"🛑 Error: Angular resolution ({args.angular_resolution_segments} segments) must be a positive integer.")
        return

    if args.start_time is not None and args.start_time < 0:
        print(f"🛑 Error: Start time ({args.start_time}s) cannot be negative.")
        return
    if args.end_time is not None and args.end_time < 0:
        print(f"🛑 Error: End time ({args.end_time}s) cannot be negative.")
        return
    if (
        args.start_time is not None
        and args.end_time is not None
        and args.start_time >= args.end_time
    ):
        print(f"🛑 Error: Start time ({args.start_time}s) must be less than end time ({args.end_time}s) for zooming.")
        return

    try:
        os.makedirs(args.output_folder, exist_ok=True)
        print(f"📂 Output directory: '{args.output_folder}' (created if it didn't exist).")
    except OSError as e:
        print(f"🛑 Error: Could not create output directory '{args.output_folder}': {e}")
        return

    files_to_process = []
    if os.path.isfile(args.input_path):
        files_to_process.append(args.input_path)
        print(f"📄 Processing single file: '{args.input_path}'")
    elif os.path.isdir(args.input_path):
        print(f"🔍 Scanning directory for files: '{args.input_path}'")
        found_files_in_dir = False
        for filename in os.listdir(args.input_path):
            full_path = os.path.join(args.input_path, filename)
            if os.path.isfile(full_path):
                files_to_process.append(full_path)
                found_files_in_dir = True
        if not found_files_in_dir:
            print(f"ℹ️ No files found in directory '{args.input_path}'.")
    else:
        print(f"🛑 Error: Input path '{args.input_path}' is not a valid file or directory.")
        return

    if not files_to_process:
        print("ℹ️ No input files to process. Exiting.")
        return

    print(f"Found {len(files_to_process)} potential file(s) to process.")
    print(f"Angular resolution set to: {args.angular_resolution_segments} segments per 360 degrees.")
    if args.start_time is not None or args.end_time is not None:
        zoom_info = []
        if args.start_time is not None:
            zoom_info.append(f"start at {args.start_time}s")
        if args.end_time is not None:
            zoom_info.append(f"end at {args.end_time}s")
        print(f"Graph X-axis will be zoomed: {' and '.join(zoom_info)}.")

    num_graphs_generated = 0
    num_logs_generated = 0
    num_skipped = 0

    for input_file in files_to_process:
        base_name = os.path.basename(input_file)
        name_part, _ = os.path.splitext(base_name)

        output_graph_filename = f"{name_part}_rpm_graph.png"
        output_graph_filepath = os.path.join(args.output_folder, output_graph_filename)

        output_log_filename = f"{name_part}_rpm_values.txt"
        output_log_filepath = os.path.join(args.output_folder, output_log_filename)

        print(f"\n--- Evaluating: {base_name} ---")
        if os.path.exists(output_graph_filepath):
            print(f"⏩ Output graph '{output_graph_filepath}' already exists. Skipping.")
            num_skipped += 1
            continue

        print(f"Processing data from: '{input_file}'...")
        timestamps, rpms_data, source_lines = process_log_file(
            input_file, args.angular_resolution_segments
        )

        if timestamps and rpms_data and source_lines:
            print(f"✔️ Successfully processed {len(timestamps)} data points from '{base_name}'.")

            plot_and_save_rpm(
                timestamps,
                rpms_data,
                args.angular_resolution_segments,
                input_file,
                output_graph_filepath,
                start_time=args.start_time,
                end_time=args.end_time,
            )
            print(f"🖼️ Plot saved to '{output_graph_filepath}'.")  # Changed emoji
            num_graphs_generated += 1

            try:
                with open(output_log_filepath, "w") as rpm_f:
                    for i in range(len(rpms_data)):
                        rpm_value = rpms_data[i]
                        source_line = source_lines[i]
                        rpm_f.write(f"RPM: {rpm_value:.2f}, FOR LINE: {source_line}\n")
                print(f"🗒️ RPM values logged to '{output_log_filepath}'.")  # Changed emoji
                num_logs_generated += 1
            except IOError as e:
                print(f"🛑 Error writing RPM log to '{output_log_filepath}': {e}")
        else:
            print(f"💡 No valid data processed or error occurred for '{base_name}'. No graph or log generated.")

    print("\n--- Processing Summary ---")
    print(f"Total files evaluated: {len(files_to_process)}")
    print(f"Graphs generated: {num_graphs_generated}")
    print(f"RPM value logs generated: {num_logs_generated}")
    print(f"Files skipped (graph already exist): {num_skipped}")
    print("✨ All processing complete.")


if __name__ == "__main__":
    main()

