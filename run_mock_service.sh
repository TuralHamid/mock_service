PYTHON_PATH=$(ls -d /usr/bin/* | grep -Eo "/usr/bin/python3.[0-9]$" | tail -1)
if [ -z "$PYTHON_PATH" ]
then
  echo "Proper Python version is not installed. Please install version 3.x"
else
  echo "Running with $PYTHON_PATH"
  nohup "${PYTHON_PATH}" mock_service.py &>/dev/null & disown
fi
