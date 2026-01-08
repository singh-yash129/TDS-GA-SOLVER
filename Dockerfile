# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the required files
COPY requirements.txt .

# Install dependencies (without cache to reduce size)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "func:app", "--host", "0.0.0.0", "--port", "8000"]
