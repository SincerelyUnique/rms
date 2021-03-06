import json

import urllib3
from flask import jsonify, request
from flask_restx import Resource

from revenues import logger, RmsConfig, db
from revenues.main import main
from revenues.models.user import User


@main.route("/jscode2session", methods=["POST"])
class WXJSCode2Session(Resource):
    def post(self):
        """ view function for validating weixin user openid """
        params = request.get_json()
        js_code = params['js_code']
        avatar_url = params['avatar_url']
        if js_code is None:
            return jsonify({"status": "failure"})
        prefix = "https://api.weixin.qq.com/sns/jscode2session?appid="
        suffix = "&grant_type=authorization_code"
        url = prefix + RmsConfig.WX_APP_ID + "&secret=" + RmsConfig.WX_APP_SECRET + "&js_code=" + js_code + suffix
        logger.info("user login, wxapp authorization: %s", url)
        retry, feedback = 3, {}
        while retry > 0:
            http = urllib3.PoolManager()
            response = http.request("GET", url)
            feedback = json.loads(response.data)
            # authorization success
            if response.status == 200 and "openid" in feedback:
                break
            retry -= 1

        if retry != 0:
            feedback["server_errcode"] = 0
            openid = feedback["openid"]
            if "session_key" in feedback:
                del feedback["session_key"]
            # query user in database
            # user_info = User.query.filter(User.openid == openid).first()
            user_info = db.session.query(User).filter(User.openid == openid).first()
            if user_info:
                feedback["isRegistered"] = True
                if user_info.audit_status == 0:
                    feedback["auditStatus"] = "pending"
                elif user_info.audit_status == 1:
                    feedback["auditStatus"] = "approved"
                elif user_info.audit_status == -1:
                    feedback["auditStatus"] = "rejected"
                feedback["role"] = "volunteer" if user_info.role == 0 else "impaired"
                # update avatarUrl when user redirect to mini program home page
                user_info.avatar_url = avatar_url
                db.session.commit()
            else:
                feedback["isRegistered"] = False
                feedback["auditStatus"] = "pending"
            feedback["status"] = "success"
            logger.info("%s: wxapp authorization success", openid)
        else:
            logger.error("wxapp authorization failed")
            feedback["status"] = "failure"
        return jsonify(feedback)


@wxapp.route("/carousel", methods=["GET"])
class GetCarouselList(Resource):
    def get(self):
        """view function for the activity_detail"""
        logger.info("query all carousel info successfully")
        return jsonify(constants.CAROUSEL_LIST)
