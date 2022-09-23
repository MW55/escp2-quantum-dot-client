FROM jupyter/minimal-notebook
SHELL ["/bin/bash", "-c"]

COPY . /app
WORKDIR /app

USER root
# Install drivers
RUN apt update && apt-get install -y libcups2 && apt-get install -y libcups2-dev && apt-get install -y libcupsimage2 && apt-get install -y libcupsimage2-dev && apt-get install -y printer-driver-gutenprint && apt upgrade -y && apt-get purge -y && apt-get clean

# Set up rights
#chmod +x ./gutenprint/unprint 
RUN mkdir /opt/notebooks && chmod -R 666 /opt/notebooks && chmod 666 /app/printing.ipynb && cp /app/printing.ipynb /opt/notebooks/ && chmod -R 666 /app/output
USER $NB_UID

RUN conda install -c conda-forge prettytable tk numpy

CMD ["jupyter", "notebook", "--notebook-dir=/opt/notebooks", "--ip='*'", "--port=8888", "--no-browser"]

