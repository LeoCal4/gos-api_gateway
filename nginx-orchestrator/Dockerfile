#
# We need a lightway image.
#
FROM python:3.6

# copying the current content
COPY . /code

# setting the workdir to code
WORKDIR /code

# performing the installation of requirements
RUN ["pip", "install", "-r", "requirements.txt"]

# Main command
CMD ["python", "main.py"]
