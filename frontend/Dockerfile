FROM python:3.11-slim

WORKDIR /code

# Copy requirements first for better caching
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY app.py /code/app.py

# Expose the default Streamlit port
EXPOSE 8501

# The command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 