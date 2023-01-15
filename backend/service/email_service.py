from database.databaseConnection import sessionLocal
from utility_data.userdata import SystemUser
from models.user import User
from models.listing import RentalListing, RentalListingUser
from fastapi_mail import FastMail, MessageType, MessageSchema
from template.email_template import CreateCustomEmailTemplate
from config.email_config import conf
from service.citites import cities
from sqlalchemy.sql import and_, text



async def FetchAllUsers() -> list:
    with sessionLocal() as session:
        return session.query(User).all()

async def SendEmail(listings, user):
    html_template = CreateCustomEmailTemplate(user.username, listings)
    fm = FastMail(conf)
    message = MessageSchema (
          subject="New rental properties available",
          recipients = [user.email],
          body = html_template,
          subtype=MessageType.html
      )
    await fm.send_message(message)

# Rental list is unordered, therefore unable to do binary search
async def SendRentalPropertyEmails():
    with sessionLocal() as session:
        all_users = await FetchAllUsers()
        for user in all_users:
            #TODO: Add property type
            property_city = user.property_city
            min_price = user.min_price
            max_price = user.max_price
            sqm = user.property_sqm

            listings_to_send = session.query(RentalListing) \
            .filter(RentalListing.listingCity == cities[property_city]) \
            .filter(and_(RentalListing.listingPrice >= min_price, RentalListing.listingPrice <= max_price)) \
            .filter(RentalListing.listingSqm >= sqm).all()

            listings_to_send_finalized = []

            # If no properties are found with the user specifications, we skip the user
           
            if len(listings_to_send) == 0:
                continue
            for listing in listings_to_send:         
                # If the listing has already been assigned to the user, we skip the user
                if session.query(RentalListingUser).filter(RentalListingUser.property_id == str(listing.id)).filter(RentalListingUser.user_id == user.id).count() > 0:
                    continue
                listings_to_send_finalized.append(listing)
                

                session.add(
                    RentalListingUser(
                        property_id = listing.id,
                        user_id = user.id
                        )
                )
                session.commit()
            await SendEmail(listings_to_send_finalized, user)


            
            
            
