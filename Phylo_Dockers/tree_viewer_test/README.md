### Instructions to setup tree_viewer_app test site

1. Run the treeviewer app first.

2. Install `nginx` in the machine.

3. Copy the **ete_pro** folder to **/var/www/** folder in the ubuntu system.

4. Change the permissions of the **ete_pro** folder using the following command. 

``sudo chmod -R 755 /var/www
``

5. Go to **/etc/nginx/sites-available** folder and create a new file named *ete_pro_config* in that folder.

6. Write the following content in the *ete_pro_config* file.

``
server {
	listen 8080;

	server_name localhost;
	root /var/www/ete_pro/public_html;
	index index.html index.htm;

	location / {
		try_files $uri $uri/ =404;
	}
}
``

7. Create a symbolic link from that file to the **sites-enabled** directory using the following command.

``
sudo ln -s /etc/nginx/sites-available/ete_pro_config /etc/nginx/sites-enabled/ 
``

8. Restart `nginx` service using the following command.

``
sudo service nginx restart
``

9. Now test the site by typing `http://localhost:8080/treeviewer_test.html` in the web browser.


