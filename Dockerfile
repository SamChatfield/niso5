FROM pklehre/niso2019-lab5

# Install / update Python 3 and pip with core pip packages
RUN apt update && apt install -y --no-install-recommends python3 python3-pip
RUN pip3 install setuptools wheel

# Set working directory
WORKDIR /usr/src/app

# Install requirements
ADD requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Add files and set entrypoint args
ADD *.py ./
CMD ["-username", "sxc678", "-submission", "python3 main.py"]
# CMD ["-username", "sxc678", "-submission", "python3 main.py", "-verbose"]
