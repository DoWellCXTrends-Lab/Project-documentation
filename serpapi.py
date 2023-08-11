from serpapi import GoogleSearch
import os, json

image_results = []

for query in ["buy instant food", "buy airpods", "buy pet supplies"]:
    params = {
        "engine": "google",               
        "q": query,                    
        "tbm": "isch",                    
        "num": "100",                     
        "ijn": 0,                        
        "api_key": os.getenv("20019fbe826a6ff37773e604eb0cc7c7d4a14a133436363a0ff0598543cb4704")
    }

    search = GoogleSearch(params)         
    images_is_present = True
    while images_is_present:
        results = search.get_dict()      
        if "error" not in results:
            for image in results["images_results"]:
                if image["original"] not in image_results:
                    print(image["original"])
                    image_results.append(image["original"])
            params["ijn"] += 1
        else:
            images_is_present = False
            print(results["error"])

print(json.dumps(image_results, indent=2))
print(len(image_results))