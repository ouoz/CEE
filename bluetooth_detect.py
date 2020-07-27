from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

print("printing...")
for address, name in devices.items():
    print("device:")
    print("name: {}, address: {}".format(name, address))
