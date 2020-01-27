### Instructions to setup tree_viewer_app test site

1. Run the treeviewer app first.

2. Install `nginx` in the machine.

3. Create a folder named **ete** inside **/var/www/** folder in the ubuntu system. 

4. Copy everything inside **ete_pro/public_html** folder into the  **/var/www/ete** folder.

5. Change the permissions of the **ete** folder using the following command. 

``sudo chmod -R 755 /var/www/ete
``

6. Go to **/etc/nginx/sites-available** folder and create a new file named *ete_pro_config* in that folder.

7. Write the following content in the *ete_pro_config* file.


```nginx
server {
	listen 8080;

	server_name _;
	root /var/www/ete;
	index index.html index.htm;

	location / {
		try_files $uri $uri/ =404;
	}
}
```

8. Create a symbolic link from that file to the **sites-enabled** directory using the following command.

``
sudo ln -s /etc/nginx/sites-available/ete_pro_config /etc/nginx/sites-enabled/ 
``

9. Restart `nginx` service using the following command.

``
sudo service nginx restart
``

10. Now test the site by typing `http://localhost:8080/treeviewer_test.html` in the web browser.

11. To test the site in public, first replace the `localhost` with the *HOSTNAME* or *IP ADDRESS* of the machine inside the following two files: **ete.js** and **treeviewer_test.html**, which are located in the **/var/www/ete** folder. Then type the above address replacing the `localhost` with *HOSTNAME* or *IP ADDRESS* in the web browser.

