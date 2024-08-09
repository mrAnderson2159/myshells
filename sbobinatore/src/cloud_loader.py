from google.cloud import storage
from src.operation import Operation
from os.path import basename
from utils import confirm


def upload(filename: str, bucket_name: str) -> str:
    """Loads a file to google cloud storage

    :param filename: relative or absolute path
    :type filename: str
    :param bucket_name: name of the bucket in google storage where to upload the file
    :type bucket_name: str
    :return: the gs://{bucket}/{blob} uri of the file
    :rtype: str
    """
    # get blob name from path
    blob_name = basename(filename)
    o = Operation('Creo storage client').start()
    # instantiate storage_client
    storage_client = storage.Client()
    o.stop().new(f'Ottengo il bucket "{bucket_name}"').start()
    # get bucket object from cloud
    bucket = storage_client.get_bucket(bucket_name)
    # set uri
    result = f"gs://{bucket_name}/{blob_name}"
    o.stop().new(f'Verifico se il blob non è presente nel cloud').start()
    # check whether if blob exists already or not
    if bucket.get_blob(blob_name) is None or confirm(
        f"il file {blob_name} è già stato caricato sul cloud, desideri sovrascriverlo"
    ):
        o.stop().new(f'Carico {filename} sul cloud').start()
        # generate blob and upload it to the cloud
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(filename)
        o.stop()
    return result
