from garminworkouts.garmin.garminclient import GarminClient
import account
import sys

print('Creating GarminClient...')
client = GarminClient(account.EMAIL, account.PASSWORD)
print('Created')
print('client type:', type(client._client))
print('is_authenticated:', client.is_authenticated)
print('display_name:', client.display_name)
print('full_name:', client.full_name)
sys.exit(0)
