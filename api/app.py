from flask import Flask, request, redirect
from app import app as your_app

def handler(req):
    return your_app(req.environ, req.start_response)
