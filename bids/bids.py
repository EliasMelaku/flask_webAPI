from flask import Flask, request
from flask.blueprints import Blueprint
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from werkzeug import cached_property

from schema import *

bids = Blueprint("bids", __name__, url_prefix="/bids")

api = Api(bids, version='1.0', title='DagmEbay API', 
          description="API for the dagm Ebay web serivce")

bid_schema = BidSchema()
bids_schema = BidSchema(many=True)

bid = api.model("Bid", {
    'BidId':fields.String,
    'AuctionId': fields.String,
    'UserId':fields.String,
    'Amount': fields.Float, 
    'Date': fields.DateTime,
}) 


@api.route('/bid/<string:bidname>')
class userResource(Resource):
    def get(self, bidId):
        # to display one bid
        bid = Bid.query.filter_by(BidId=bidId).first()
        return bid_schema.dump(bid)
    
    # to update an bid
    @api.expect(bid)
    @api.response(204, 'bid updated')
    def put(self, bidname):
        bid = Bid.query.filter_by(bidName=bidname).first()
        # bid.bidId = "1"
        bid.BidId = request.json['BidId']
        bid.AuctionId = request.json['AuctionId']
        bid.UserId = request.json['UserId']
        bid.Amount = request.json['Amount']
        bid.Date = datetime.now()
        
        db.session.add(bid)
        db.session.commit()
        
        return bid_schema.dump(bid)
    
    #to remove an bid
    @api.response(204, 'bid successfully deleted.')
    def delete(self, bidId):
        """
        Deletes Bid.
        """
        bid = Bid.query.filter_by(BidId=bidId).first()
        if bid is None:
            return None, 404
        db.session.delete(bid)
        db.session.commit()
        return None, 204
        
@api.route('/bids')
class userResource(Resource):
    # get all the itmes
    def get(self):
        """
        Get all the bids
        """
        bids = Bid.query.all()
        return bids_schema.dump(bids)
    
    @api.expect(bid)
    def post(self):
        # creates a new user
        
        new_bid = Bid()
        new_bid.BidId = request.json['BidId']
        new_bid.AuctionId = request.json['AuctionId']
        new_bid.UserId = request.json['UserId']
        new_bid.Amount = request.json['Amount']
        new_bid.Date = datetime.now()
        
        db.session.add(new_bid)
        db.session.commit()
        
        return bid_schema.dump(new_bid)