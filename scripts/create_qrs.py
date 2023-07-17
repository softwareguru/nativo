
def main():
    import csv, sys, os, qrcode
    from slugify import slugify

    print("Starting ...")
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    else:
        source_file = "badges.csv"


    try:
        os.mkdir("qr")
    except FileExistsError:
        pass
    except OSError:
        print ("Creation of the directory qr failed" )
    else:
        print ("Created directory ...")

    with open(source_file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            company = row['company']
            title = row['title']
            email = row['email']

            data = f'''BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name}
FN:{first_name} {last_name}
ORG:{company}
EMAIL:{email}
END:VCARD'''


            qr = qrcode.QRCode(version=5)
            qr.add_data(data)
            qr.make()
            img = qr.make_image()
            slug = slugify(first_name)+"-"+slugify(last_name)
            img.save(f"qr/{slug}.png")

    print("Done")

if __name__ == "__main__": 
	main() 
