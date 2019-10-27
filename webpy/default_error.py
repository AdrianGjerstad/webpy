error_data = $status + ' ' + $explain_code($status)
message = 'Requesting for the file at ' + $request.path ' resulted in an error.'

$output.write('''
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-width=1.0'>
    <title>Error %s</title>
  </head>
  <body>
    <h1>Error %s</h1>
    <p>Error Code: %i</p>
    <p>Message: %s</p>
  </body>
</html>
''' % (error_data, error_data, $status, message))