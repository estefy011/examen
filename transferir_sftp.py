import paramiko

SFTP_HOST = 'localhost'
SFTP_PORT = 22
SFTP_USER = 'usuario'
SFTP_PASSWORD = 'usuario'
LOCAL_FILE = 'nuevos_clientes.csv'
REMOTE_PATH = 'C:/Users/Estefania/Destino/nuevos_clientes.csv'

try:
    print("Conectando al servidor SFTP...")
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print("Conexión establecida.")

    print(f"Subiendo archivo {LOCAL_FILE} a {REMOTE_PATH}...")
    sftp.put(LOCAL_FILE, REMOTE_PATH)
    print(f"Archivo transferido exitosamente a {REMOTE_PATH}.")

    sftp.close()
    transport.close()
    print("Conexión cerrada.")

except Exception as e:
    print(f"Error durante la transferencia: {e}")
