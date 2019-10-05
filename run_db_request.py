import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import boto3
import document_db

#Define CSS file and Dash app instance
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF', #'#111111',
    'text': '#4285F4'
}

s3_client = boto3.client('s3')

#Get document instance
doc_db = document_db.DocumentDB('documents','texts')   

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div(style={'backgroundColor': colors['background']}, 
  children=[
    html.I("Type your request here:", style={'textSize':'10pt'}),
    html.Br(),
    dcc.Input(id="input_request", type="text", value="online",
        style={'width':'30%','display': 'inline-block'}),
    html.Br(), 
    html.Hr(),
    html.H1('Results', style={'textAlign':'center', 'color': colors['text']}),
    html.Div([
        html.H3(children='Documents found'),
        html.Table(id='my-table'),
        html.H5(children='Document to show:'),
        dcc.Dropdown(id='docs-dropdown'),
        html.Div(id='display-selected-values')], 
        style={'width':'25%','display': 'inline-block'}), 
    html.Div([
        html.H3('Original document'),
        html.Img(id='my-image', style={'width':'80%','height':'80%'}),
    ], style={'width':'50%','display': 'inline-block','float':'right'})
])

@app.callback([Output('my-table', 'children'),
               Output('docs-dropdown', 'options'),
               Output('display-selected-values', 'children')],
              [Input('input_request', 'value')])
def table_update(request):
    results = doc_db.search_for_docs(request)
    df = pd.DataFrame(results)
    df_show = pd.DataFrame()
    dropdown_menu = []
    text = ''
    if len(df)>0:
        #df = df.iloc[:int(num)]
        df['document_name'] = df['file_name'].apply(lambda x: 
                            html.A(x, href=s3_client.generate_presigned_url('get_object', 
                            Params={'Bucket':'document360', 'Key':x}), target="_blank"))
        df['matching_score'] = df.score.round(3)
        df_show = df[['document_name','matching_score']].iloc[:int(10)]
        dropdown_menu = [{'label': i, 'value': i} for i in df.file_name.values]
        text = u'{} documents found'.format(len(df))
    return generate_table(df_show), dropdown_menu, text

@app.callback(
    Output('docs-dropdown', 'value'),
    [Input('docs-dropdown', 'options')])
def set_docs_value(available_options):
    if available_options != None and len(available_options)>0:
        return available_options[0]['value']
    else:
        return ''

@app.callback(Output('my-image', 'src'), [Input('docs-dropdown', 'value')])
def doc_update(value):
        img_link = s3_client.generate_presigned_url('get_object', 
                Params={'Bucket':'document360', 'Key':value})
        return img_link 

if __name__ == '__main__':
    app.run_server(debug=False)

