from s3_utils import get_s3_keys, read_image_from_s3

import dash
import dash_html_components as html
import base64

app = dash.Dash()

img = read_image_from_s3('document360', '1.jpg')
#image_filename = 'my-image.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())
encoded_image = img #base64.b64encode(img)

app.layout = html.Div([
    html.Img(id='image', src='https://document360.s3.amazonaws.com/1.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIATZNK4QN5LKQTZTNI%2F20191004%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20191004T231335Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=1a0b9641aed963b40610fe123ee0c654bb69725297dea1ea62950cf7b47ae73c',
    style={
        'height': '20%',
        'width': '20%'
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)
