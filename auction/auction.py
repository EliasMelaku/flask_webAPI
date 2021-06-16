from flask import Flask, request
from flask.blueprints import Blueprint
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from werkzeug import cached_property

from schema import *

auctions = Blueprint("auction", __name__, url_prefix="/auction")

api = Api(auctions, version='1.0', title='DagmEbay API', 
          description="API for the dagm Ebay web serivce")

auction_schema = AuctionSchema()
auctions_schema = AuctionSchema(many=True)

auction = api.model("Auction", {
    'AuctionId':fields.String,
    'ItemId': fields.String,
    'StartDate':fields.DateTime,
    'EndDate': fields.DateTime, 
    'InitialPrice': fields.Float,
    'CurrentPrice': fields.Float,
    'IsCompleted': fields.Boolean,
    'HigestBidder': fields.String
}) 


@api.route('/auction/<string:auctionId>')
class userResource(Resource):
    def get(self, auctionId):
        # to display one user
        user = Auction.query.filter_by(AuctionId=auctionId).first()
        return auction_schema.dump(user)
    
     # to update an auction
    @api.expect(auction)
    @api.response(204, 'Auction updated')
    def put(self, auctionId):
        auction = Auction.query.filter_by(AuctionId=auctionId).first()
        # item.ItemId = "1"
        auction.ItemName = request.json['ItemName']
        auction.Category = request.json['Category']
        auction.Description = request.json['Description']
        auction.Image = request.json['Image']
        auction.SellerId = request.json['SellerId']
        
        db.session.add(auction)
        db.session.commit()
        
        return auction_schema.dump(auction)
    
    #to remove an auction
    @api.response(204, 'Auction successfully deleted.')
    def delete(self, auctionId):
        """
        Deletes Dinner.
        """
        auction = Auction.query.filter_by(AuctionId=auctionId).first()
        if auction is None:
            return None, 404
        db.session.delete(auction)
        db.session.commit()
        return None, 204
    
    
@api.route('/auction')
class userResource(Resource):
    def get(self):
        """
        Get all the auctions
        """
        items = Item.query.all()
        return auctions_schema.dump(items)
    
    @api.expect(auction)
    def post(self):
        # creates a new user
        
        new_auction = auction()
        new_auction.AuctionId = "1"
        new_auction.ItemId = request.json['ItemId']
        new_auction.StartDate = request.json['StartDate']
        new_auction.EndDate = request.json['EndDate']
        new_auction.InitialPrice = request.json['InitialPrice']
        new_auction.CurrentPrice = request.json['CurrentPrice']
        new_auction.IsCompleted = request.json['IsCompleted']
        new_auction.HigestBidder = request.json['HighestBidder']
        
        db.session.add(new_auction)
        db.session.commit()
        
        return auction_schema.dump(new_auction)