import shiny
import pandas as pd

df = pd.read_csv('/content/drive/MyDrive/HHS_Provider_Relief_Fund.csv')

ui = shiny.ui.page(
    shiny.ui.sidebar(
        shiny.ui.select('state', 'Select a state:', df['state'].unique())
    ),
    shiny.ui.mainPanel(
        shiny.ui.plotlyOutput('plot')
    )
)

server = shiny.server.ModuleServer(
    ui,
    shiny.render.plotlyOutput('plot', callback=function(input, output, session):
        state = input['state']
        df_filtered = df[df['state'] == state]
        output$plot = shiny.plotly.plot_ly(x=df_filtered['measure'], y=df_filtered['value'], type='bar')
)

shiny.run(server)
