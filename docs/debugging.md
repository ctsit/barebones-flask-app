# Creating SSL certificates for debugging

When developing the app we want to avoid the annoying message about
unsafe certificate. To accomplish that generate a self-signed certificate in
the ssl folder:

<pre>
cd ssl
./gen_cert.sh
</pre>
