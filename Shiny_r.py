from shiny import App, render, ui
import matplotlib.pyplot as plt
import pandas as pd

csv_file_path = ['/content/drive/MyDrive/HHS_Provider_Relief_Fund.csv']
df = pd.read_csv('/content/drive/MyDrive/HHS_Provider_Relief_Fund.csv')

df_binge = df[(df['MeasureId']  == 'BINGE') & (df['Data_Value_Type'] == 'Age-adjusted prevalence')]

counties = df_binge['Provider Name'].unique()

app_ui = ui.page_fluid(
    ui.input_select("state", "Select State", {state: state for states})
    ui.output
)

app_ui = ui.page_fluid(
    ui.input_select("state", "Select State", {state: state for states}),
    ui.output_text_verbatim("avg_data_value"),
    ui.output_plot("bar_chart")
)

def server(input, output, session):

  @output
  @render.text
  def avg_data_value():
    selected_state = input.state()
    avg_value = df_binge[df_binge['Provider Name'] == selected_state]['Data_Value'].mean()
    return f"HHS Provider Relief Fund Comparison for {selected_state}:"

    @output
    @render.plot(alt="Binge Drinking Age-adjusted Prevalence Bar Chart")
    def bar_chart():
        overall_avg = df_binge['Data_Value'].mean()
        selected_county_avg = df_binge[df_binge['Provider Name'] == input.state()]['Data_Value'].mean
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(['Selected State', 'Overall Avergage'], [selected_county_avg, overall_avg], color=['Light'])

        ax.set_ylabel('Data Vlue (Age-adjusted prevalence) - Percent')
        ax.set_ylim(0, 30)
        ax.set_title('HHS Provider Relief Fund Comparison')

        return fig

app = App(app_ui, server, debug=True)