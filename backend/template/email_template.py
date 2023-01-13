
def CreateHtmlForProperty(property):
    property_string = f"""
                      <h1> {property.listingName}
                      <h1> Rental in: {property.listingCity}, {property.listingAdress} </h1>
                      <h2> Pricing: {property.listingPrice} </h2>
                      <h2> Rental Size: {property.listingSqm} | Rental rooms: {property.listingRooms} </h2>
                      """ 
    return property_string


def CreateCustomEmailTemplate(user, properties):
    html_string = f"""
                      <h1> Hello {user}. Here are the newest properties that fall under your requirements: </h1>
                    """
    for i in range(len(properties)):
        html_string += CreateHtmlForProperty(properties[i])
    return html_string



