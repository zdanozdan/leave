NameVirtualHost *:80
<VirtualHost *:80>
   ServerName www.urlopy.mikran.com
   ServerAlias urlopy.mikran.com
   ServerAdmin admin@mikran.pl

   WSGIScriptAlias / /home/mikran/mikran.com/leave/mleave/wsgi.py

   DocumentRoot /home/mikran/mikran.com/leave/

   <Directory /home/mikran/mikran.com/leave/mleave>
   <Files wsgi.py>
     Order allow,deny
     Allow from all
   </Files>
   </Directory>

   <Directory /home/mikran/mikran.com/leave/static>
      Order allow,deny
      Allow from all
   </Directory>

   Alias /static /home/mikran/mikran.com/leave/static

   ErrorLog /home/mikran/mikran.com/logs/error.log
   CustomLog /home/mikran/mikran.com/logs/access.log combined
</VirtualHost>