<br>
<h3>Installation -</h3> 
<ul>
	<li>python==2.7</li>
	<li>django==1.11.20</li>
	<li>pillow</li>
	<li>django-storages</li>
	<li>boto3</li>
</ul>
<br>
<h1>Book Explorer</h1>
<br>
<p>A web application that allows the user to upload a csv files contining books</p>
<br>
<p>Books coloumns must be in this order</p>
<ol>
	<li>Book Title</li>
	<li>Book Author</li>
	<li>Date Published</li>
	<li>Book ID</li>
	<li>Publisher</li>
</ol>
<p>Each row of the csv needs to be in the following format:</p>
<ol>
	<li>Title: String format</li>
	<li>Author: String format</li>
	<li>Published: Date format, dd/mm/yyyy</li>
	<li>ID: Integer format, needs to be unique for every entry</li>
	<li>Publisher: String format</li>
</ol>
<br>
<p>If any of the book ids in the csv file is not unique then the upload will be stopped before it reaches the backend</p>
<br>
<p>When a book is uploaded it is sent to an aws s3 bucket. Rather than saving it in the application</p>
<br>
<p>After the upload the user will be redirected to a page with the uploaded file as the title and the uploaded file contents in a table</p>
<br>
<p>The user can login at any time view their list of uploaded csv files and inpect the contents of each one</p>

