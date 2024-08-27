# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

# Check if PyQt5 is installed
python3 -c "import PyQt5" &> /dev/null
if [ $? -ne 0 ]; then
    echo "PyQt5 is not installed. Installing PyQt5..."
    pip3 install PyQt5
    if [ $? -ne 0 ]; then
        echo "Failed to install PyQt5. Please check your Python and pip installation."
        exit 1
    fi
    echo "PyQt5 has been successfully installed."
else
    echo "PyQt5 is already installed."
fi

# Check if pynput is installed
python3 -c "import pynput" &> /dev/null
if [ $? -ne 0 ]; then
    echo "pynput is not installed. Installing pynput..."
    pip3 install pynput
    if [ $? -ne 0 ]; then
        echo "Failed to install pynput. Please check your Python and pip installation."
        exit 1
    fi
    echo "pynput has been successfully installed."
else
    echo "pynput is already installed."
fi