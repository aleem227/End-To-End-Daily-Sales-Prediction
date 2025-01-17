# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the SQL query and subsequent scripts
RUN python download_db.py && \
    python sql_query.py && \
    python data-engineering.py && \
    python data_analysis.py && \
    python model_training.py

# Run pytest to execute tests
RUN pytest tests/

# Run uvicorn when the container launches
CMD ["uvicorn", "model_prediction:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
