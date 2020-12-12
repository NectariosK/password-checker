#Password checker project
#This code basically checks if a certain password has been leaked
'''
Some important link below.
		1. Link to a website to check if any of your passwords have been leaked--->https://haveibeenpwned.com/Passwords
		2. Sha1 Hash generator--->https://passwordsgenerator.net/sha1-hash-generator/
'''
import requests
import hashlib
import sys

def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char #hash the first 4 characters for security reasons
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
	return res
'''
def read_res(response):
	print(response.text)
'''

#instead of a read response function let's get one that gets the passwords
def get_password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(':')for line in hashes.text.splitlines())
	#print(hashes)
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0
		#print(h, count)

def pwned_api_check(password):
	#check password if it exists in API response ##API in full: Application Programming Interface
	#print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())# check the sha1 password in gibberish
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char, tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5_char)
	#print(response)
	#print(first5_char, tail)
	#return read_res(response)
	return get_password_leaks_count(response, tail)

#pwned_api_check('123')
#print(res)
def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f'{password} was found {count} times... you should probably change your pasword')
		else:
			print(f'{password} was NOT found. Carry on!')
	return 'done!'

if __name__=='__main__':
	#main(sys.argv[1:]) #this works properly
	sys.exit(main(sys.argv[1:])) #line of code basically to exit if this doesn't exit---then, exit the whole process