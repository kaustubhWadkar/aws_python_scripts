import json
from datetime import datetime
from datetime import date
from datetime import datetime
from collections import defaultdict

# read json file
today = date.today()
print(today)
with open("bucket.json", "r") as file:
    data = json.load(file)

bucket_name = data["buckets"]
#print(bucket_name)

# Print a summary of each bucket: Name, region, size (in GB), and versioning status

for b in bucket_name:
    Name = b.get('name', None)
    region = b.get('region', None)
    size = b.get('sizeGB', None)
    version_status = b.get('versioning', None)
    print(f""" Summary of {Name}
         Name is {Name}
         region is {region}
         size in GB  is {size}
         version_status is {version_status}
        -----------------------------------

""")
    
#####  buckets which are not useed in last 90 days

buk_access = {}
bukcetAcc = []

buckets_nt_useed = []

for b in bucket_name:
     Name = b.get('name', None)
     Last_acc = b.get('lastAccessed', None)
 
     buk_access['Name'] = Name
     buk_access['last_accessed'] = Last_acc
     bukcetAcc.append(buk_access)

print(bukcetAcc)
#Identify buckets larger than 80 GB from every region which are unused for 90+ days.
for b in bucket_name:
    Last_acc = b.get('lastAccessed', None)
    size = b.get('sizeGB', None)
    last_acc = datetime.strptime(Last_acc, '%Y-%m-%d').date()
    diff = today - last_acc
    diff = diff.days
    print(diff)
    if diff > 90 and size > 80  :
        buckets_nt_useed.append(b.get('name'))
    else:
        pass

print(buckets_nt_useed)

#Generate a cost report: total s3 buckets cost grouped by region and department.
total_cost = 0
for b in bucket_name:
    size = b.get('sizeGB', None)
    cost = 0.023 * size
    total_cost += cost

print("total s3 bucket cost",total_cost)
cost_by_region = {}
COST_PER_GB = 0.023
for b in bucket_name:
    size = b.get('sizeGB', None)
    Name = b.get('name', None)
    region = b.get('region', None)
    dep = b.get('tags', {}).get('team', None)
    cost = size * COST_PER_GB


    cost_by_region.setdefault(region, {}).setdefault(dep, {'total_cost': 0, 'buckets': []})
    cost_by_region[region][dep]['total_cost'] += cost
    cost_by_region[region][dep]['buckets'].append(b.get('name'))

for region, deps in cost_by_region.items():
    print(f"\nRegion: {region}")
    for dep, info in deps.items():
        print(f"  Department: {dep}")
        print(f"    Buckets: {', '.join(info['buckets'])}")
        print(f"    Total Cost: ${info['total_cost']:.2f}")









