# Grab Python 3.9
FROM python:3.9

# Set the Working DIR
WORKDIR /bot

# Copy the requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Install the Python requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the src code to the app
COPY ./src .

# Run the Bot and API
CMD ["python", "-O", "bot.py"]