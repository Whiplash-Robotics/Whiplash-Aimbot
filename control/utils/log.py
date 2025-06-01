import serial
import datetime
import time
import argparse
import os

def main():
    """Main function to listen to serial port and log data, configured by CLI arguments."""

    parser = argparse.ArgumentParser(description="Log data from a serial port to timestamped files.")
    parser.add_argument(
        "output_dir",
        nargs="?", # Makes the argument optional
        default="../outputs", # Default output directory
        help="Directory where log files will be saved. Default: ../outputs"
    )
    parser.add_argument(
        "port",
        nargs="?",
        default="COM3", # Default serial port
        help="Serial port name (e.g., COM3, /dev/ttyUSB0). Default: COM3"
    )
    parser.add_argument(
        "baud_rate",
        nargs="?",
        type=int,
        default=115200, # Default baud rate
        help="Baud rate for serial communication (e.g., 9600, 115200). Default: 115200"
    )

    args = parser.parse_args()

    output_dir = args.output_dir
    port = args.port
    baud_rate = args.baud_rate

    output_file = None
    logging_active = False

    # Ensure the output directory exists
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
    except OSError as e:
        print(f"Error: Could not create output directory {output_dir}. Details: {e}")
        print("Please check permissions or create the directory manually.")
        return # Exit if directory cannot be created

    print(f"Output directory: {os.path.abspath(output_dir)}")
    print(f"Attempting to connect to {port} at {baud_rate} baud...")

    try:
        ser = serial.Serial(port, baud_rate, timeout=None) # Blocking read
        print(f"Successfully connected to {port}. Waiting for data...")
        time.sleep(2) # Give Arduino a moment to reset
        ser.flushInput()

        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()

                    if line:
                        print(f"Received: {line}")

                        if line == "LOGGING_START":
                            if logging_active and output_file:
                                print("LOGGING_START received while already logging. Closing previous file and starting new.")
                                output_file.close()

                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            # Use os.path.join for creating platform-independent paths
                            filename_only = f"out_{timestamp}.txt"
                            full_filepath = os.path.join(output_dir, filename_only)

                            try:
                                output_file = open(full_filepath, "w")
                                logging_active = True
                                print(f"--- Logging started to {full_filepath} ---")
                                output_file.write(f"# Log started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                output_file.write(f"# Data from port: {port} at {baud_rate} baud\n")
                                output_file.write(line + "\n")
                            except IOError as e:
                                print(f"Error: Could not open file {full_filepath} for writing: {e}")
                                logging_active = False
                                output_file = None

                        elif line == "LOGGING_STOP":
                            if logging_active and output_file:
                                print(f"--- Logging stopped for {output_file.name} ---")
                                output_file.write(line + "\n")
                                output_file.write(f"# Log stopped at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                output_file.close()
                                output_file = None
                                logging_active = False
                            elif not logging_active:
                                print("Received LOGGING_STOP without an active logging session. Ignoring.")

                        elif logging_active and output_file:
                            output_file.write(line + "\n")
                            output_file.flush()

            except serial.SerialException as e:
                print(f"Serial error: {e}")
                print("Attempting to reconnect in 5 seconds...")
                if output_file:
                    output_file.close()
                    output_file = None
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
                print("\nExiting program by user request.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                time.sleep(1)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}. Details: {e}")
        print("Please check the port name, ensure the Arduino is connected,")
        print("and that no other program is using the port (e.g., Arduino IDE Serial Monitor).")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")
        if output_file:
            print(f"Closing active log file: {output_file.name}")
            output_file.close()

if __name__ == "__main__":
    main()
