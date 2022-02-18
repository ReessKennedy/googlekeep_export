# Google Keep Export Option

## Problem
* Google Keep is a fine app for very quickly logging & collecting thoughts, ideas, links & images while on the go on my phone or while in the browser using the extension but I don't find it great for sorting and prioritizing these ideas later. 
* Meanwhile, there are many tools that are great for prioritizing notes (Notion, Airtable, Seatable, Baserow, Raindrop.io) but don't have great methods for capturing notes and ideas. These database-like apps do have have APIS though ... 

## Solution
* A script to export all images from GoogleKeep to a folder
* A script to exprt all note text and meta to a Json file and reference the exported images

## Methods
* [Google Keep's official API is here](http://https://developers.google.com/keep/api/reference/rest "Google Keep's official API is here") but seems to be restricted to Enterprise -- or that you need to use a GSuite account
* [I use the unofficial to export images](https://github.com/kiwiz/gkeepapi "I use the unofficial to export images") and note data to Json.
* [StackOverflow discussion here](https://stackoverflow.com/questions/19196238/is-there-a-google-keep-api "StackOverflow discussion here")


## Specific

1. You'll have to have Python installed and install pip
2. Install Kiwiz's Gkeep Api Wrapper with `pip install gkeepapi` and [check out the documentation here](https://gkeepapi.readthedocs.io/en/latest/ "check out the documentation here") ...
3. You're normal login/pass for Google Keep won't work so you need to create a speciall "App Password" and can find out [more info on that here](https://support.google.com/accounts/answer/185833?hl=en "more info on that here"). 
4. Place your login and pass in creds.py
5. You may have to use PIP to install some additional stuff so just follow prompts
6.  "keep_images.py" exports all images to a path outside this directory but you can chaneg it to anything
7. "keep_json.py" exports all notes that are not pinned or archives to a JSON file and then archives all the notes once this is done. You can easily edit this to include pinned notes and/or not archive after. 
8. Once all is exported you can go wild importing to Notion or Airtable or anywhere ... this could be extended to insert this data directly but exporting to JSON makes it flexible. I added some empty folders where code for integrations code be added.
9. I also created some simple web triggers to do this work using PHP since it's easy to trigger PHP 


```php
function executeAsyncShellCommand($comando = null) {
   if(!$comando){
       throw new Exception("No command given");
   }
   // If windows, else
   if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
       system($comando." > NUL");
   }else{
       shell_exec("/usr/bin/nohup ".$comando." >/dev/null 2>&1 &");
   }
}

$command = escapeshellcmd('python3 /www/wwwroot/yourdomainname.com/gkeep/keep_images.py');

// Normal way, have to wait ...
// $output = shell_exec($command);

// A synce way, don't have to wait ... 
executeAsyncShellCommand($command);

echo $output;
echo 'Nice';
```
