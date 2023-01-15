from premailer import transform

def CreateHtmlForProperty(property):

    print(property.listingName)
    property_string = f"""
                    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px auto; box-shadow: 2px 2px 8px #ccc; border-radius: 5px; background-color: #f5f5f5; width: max-content; text-align:center;">
                        <h2 style="margin-top: 0; font-size: 20px; font-weight: normal;">{property.listingName}</h2>
                        <p style="margin: 5px 0; font-size: 14px;>{property.listingCity}</p>
                        <p style="margin: 5px 0; font-size: 14px;>Size: {property.listingSqm} sqm</p>
                        <a href="{property.listingUrl}" style="background-color: #0000ff; color: #fff; padding: 10px 20px; border-radius: 5px; text-decoration: none; margin-top: 10px; display: inline-block; font-size: 14px;">View listing</a>
                    </div>
                      """ 
    return property_string


def CreateCustomEmailTemplate(user, properties):
    html_string = """
            <html>
              <head>
                <link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
              </head>

            <body style="font-family: 'Roboto', Arial, sans-serif;">
            <h1> Greetings! Here are the newest listings that meet your requirements:
            """
    for i in range(len(properties)):
        html_string += CreateHtmlForProperty(properties[i])

    html_string += """</body>
                      </html>
                   """
    final_html = transform(html_string)
    return final_html




