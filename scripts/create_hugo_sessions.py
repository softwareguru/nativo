# Script to create the session content files for Hugo from a csv file.

def main():
    import csv, sys, os
    from slugify import slugify
    
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    else:
        source_file = "sessions.csv"

    event_slug = "mayo-2023"

    dirname = "sessions/"+event_slug
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass
    except OSError:
        print ("Creation of the directory "+dirname+" failed" )


    with open(source_file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id = row['id']
            title = row['title']
            speakers = row['speakers'].split(", ")
            format = row['format']
            block = row['block']
            time_start = row['time_start']
            time_end = row['time_end']
            abstract = row['description']
            video = row['video']
            slides = row['slides']
            
            slug = slugify(title)
            filename =  f"sessions/{event_slug}/{id}-{slug}.md"

            with open(filename, "w") as f:
                f.write("---\n")
                f.write(f"id: \"{id}\"\n")
                f.write(f"title: \"{title}\"\n")
                f.write(f"slug: {slug}\n")
                f.write("speakers:\n")
                for s in speakers:
                    f.write(f" - {s}\n")
                f.write(f"format: {format}\n")
                f.write(f"block: {block}\n")
                f.write(f"time_start: {time_start}\n")
                f.write(f"time_end: {time_end}\n")
                f.write(f"slides: \n")
                f.write(f"video: \n")
                f.write("---\n\n")
                f.write(abstract)


if __name__ == "__main__": 
	main() 

