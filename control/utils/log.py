import argparse
import datetime
import os
import time

import serial


def main():
    """Main function to listen to serial port and log data, configured by CLI arguments."""

    parser = argparse.ArgumentParser(
        description="Log data from a serial port to timestamped files."
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="../outputs/raw",  # Default output directory
        help="Directory where log files will be saved. Default: ../outputs/raw",
    )
    parser.add_argument(
        "port",
        nargs="?",
        default="COM3",
        help="Serial port name (e.g., COM3, /dev/ttyUSB0). Default: COM3",
    )
    parser.add_argument(
        "baud_rate",
        nargs="?",
        type=int,
        default=115200,
        help="Baud rate for serial communication (e.g., 9600, 115200). Default: 115200",
    )

    args = parser.parse_args()

    output_dir = args.output_dir
    port = args.port
    baud_rate = args.baud_rate

    output_file = None
    current_log_filepath = None  # To store the path of the currently open log file
    logging_active = False

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
    except OSError as e:
        print(f"Error: Could not create output directory {output_dir}. Details: {e}. Please check permissions or create the directory manually.")
        return

    print(f"Output directory: {os.path.abspath(output_dir)}")
    print(f"Attempting to connect to {port} at {baud_rate} baud...")

    try:
        ser = serial.Serial(port, baud_rate, timeout=None)
        print(f"Successfully connected to {port}. Waiting for data...")
        time.sleep(2)
        ser.flushInput()

        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode("utf-8", errors="ignore").strip()

                    if line:
                        print(f"Received: {line}")

                        if line == "LOGGING_START":
                            if logging_active and output_file:
                                print("LOGGING_START received while already logging. Closing previous file and starting new.")
                                output_file.close()
                                # No need to delete previous file here, as it was a completed session or an old partial one.

                            timestamp = datetime.datetime.now().strftime(
                                "%Y%m%d_%H%M%S"
                            )
                            filename_only = f"out_{timestamp}.txt"
                            current_log_filepath = os.path.join(
                                output_dir, filename_only
                            )

                            try:
                                output_file = open(current_log_filepath, "w")
                                logging_active = True
                                print(
                                    f"--- Logging started to {current_log_filepath} ---"
                                )
                                output_file.write(
                                    f"# Log started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                )
                                output_file.write(
                                    f"# Data from port: {port} at {baud_rate} baud\n"
                                )
                                output_file.write(line + "\n")
                            except IOError as e:
                                print(
                                    f"Error: Could not open file {current_log_filepath} for writing: {e}"
                                )
                                logging_active = False
                                output_file = None
                                current_log_filepath = None  # Reset if open failed

                        elif line == "LOGGING_STOP":
                            if logging_active and output_file:
                                print(f"--- Logging stopped for {output_file.name} ---")
                                output_file.write(line + "\n")
                                output_file.write(
                                    f"# Log stopped at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                )
                                output_file.close()
                                output_file = None
                                current_log_filepath = (
                                    None  # Current session ended successfully
                                )
                                logging_active = False
                            elif not logging_active:
                                print("Received LOGGING_STOP without an active logging session. Ignoring.")

                        elif logging_active and output_file:
                            output_file.write(line + "\n")
                            output_file.flush()

            except serial.SerialException as e:
                print(f"Serial error: {e}. Attempting to reconnect in 5 seconds...")
                if output_file:
                    output_file.close()  # Close the file
                    # Decide if you want to delete a partial file on serial error or keep it
                    # For now, let's keep it, as it wasn't a user interrupt.
                    # If you want to delete:
                    # if current_log_filepath and os.path.exists(current_log_filepath):
                    #     print(f"Deleting partial file due to serial error: {current_log_filepath}")
                    #     os.remove(current_log_filepath)
                    output_file = None
                    current_log_filepath = None
                logging_active = False
                time.sleep(5)
                try:
                    if ser.is_open:
                        ser.close()
                    ser.open()
                    print(f"Reconnected to {port}.")
                    ser.flushInput()
                except Exception as recon_e:
                    print(f"Failed to reconnect: {recon_e}. Exiting.")
                    break

            except KeyboardInterrupt:
                print("\nKeyboardInterrupt received. Exiting program.")
                if logging_active and output_file and current_log_filepath:
                    print(f"Closing and deleting incomplete log file: {current_log_filepath}")
                    output_file.close()  # Close it first
                    if os.path.exists(current_log_filepath):
                        try:
                            os.remove(current_log_filepath)
                            print(f"Successfully deleted {current_log_filepath}")
                        except OSError as e_del:
                            print(
                                f"Error deleting file {current_log_filepath}: {e_del}"
                            )
                elif output_file:  # If file was somehow open but not logging_active
                    output_file.close()
                logging_active = False  # Ensure logging stops
                break  # Exit the main while loop
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                # Consider if the current file should be closed/deleted on other errors too
                time.sleep(1)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}. Details: {e}. Please check the port name, ensure the Arduino is connected, and that no other program is using the port (e.g., Arduino IDE Serial Monitor).")
    finally:
        if "ser" in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")
        # This final check for output_file is mostly for unexpected exits
        # The KeyboardInterrupt handler should ideally handle its specific case.
        if output_file and not output_file.closed:
            print(f"Ensuring active log file is closed: {output_file.name}")
            output_file.close()
            # If exiting here and it was an active logging session that wasn't handled by KeyboardInterrupt,
            # you might also consider deleting current_log_filepath if it exists and logging was active.
            # However, the KeyboardInterrupt logic is the primary place for that specific cleanup.


if __name__ == "__main__":
    main()
