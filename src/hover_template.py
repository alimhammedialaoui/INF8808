
dictionary = {'IC':'Impôt corporatif',
              'IP':'Impôt au particulier',
              'TVQ':'Taxe de vente du Québec',
              'RAS':'Retenues à la source',
              'IC_P':'Impôt corporatif',
              'IP_P':'Impôt au particulier',
              'TVQ_P':'Taxe de vente du Québec',
              'RAS_P':'Retenues à la source',
              'IC_C':'Impôt corporatif',
              'IP_C':'Impôt au particulier',
              'TVQ_C':'Taxe de vente du Québec',
              'RAS_C':'Retenues à la source',
            }

def clustered_barchart_hover_template(laws):
    '''
        Sets the template for the hover tooltips on the neighborhoods.

        The label is simply the name of the neighborhood in font 'Oswald'.

        Returns:
            The hover template.
    '''
    label1 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Loi : " '</span>'
    value1 = '<span style="font-family:Oswald">' + '%{x}' + '<br>' 
    
    label2 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Taux de respect : " '</span>'
    value2 = '<span style="font-family:Oswald">' + ' %{y:.2f} % <br>' 
    
    return label1 + value1 + label2 + value2 + '<extra></extra>'


def stacked_barchart_hover_template():
    label1 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Année : " '</span>'
    value1 = '<span style="font-family:Oswald">' + '%{x}' + '<br>' 

    label2 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Taux de respect : " '</span>'
    value2 = '<span style="font-family:Oswald">' + ' %{y:.2f} % <br>' 

    label3 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Taux Maximum Possible : " '</span>'
    value3 = '<span style="font-family:Oswald">' + ' %{customdata[0]:.2f} % <br>' 

    label4 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Nombre total d'entreprises : " '</span>'
    value4 = '<span style="font-family:Oswald">' + ' %{customdata[1]:,} <br>' 

    return label1 + value1 + label2 + value2 + label3 + value3 + label4 + value4 + '<extra></extra>'

def bubblechart_hover_template():
    label1 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Règle : " '</span>'
    value1 = '<span style="font-family:Oswald">' + '%{x}' + ' = ' + '%{y}' + '<br>' 
    
    label2 = '<span style="font-family:' + "'Oswald'" + '; font-weight:bold">' + " Proportion : " '</span>'
    value2 = '<span style="font-family:Oswald">' + '%{text}' + '<br>' 

    return label1 + value1 + label2 + value2 + '<extra></extra>'