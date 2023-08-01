FROM python:3.9
# Install python and pip
COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Add our code
COPY . /app
WORKDIR /app

# Run the image
CMD streamlit run --server.port $PORT app.py