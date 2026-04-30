from flask import Blueprint, render_template, request, jsonify, session
from src.database.models import db, User
from werkzeug.security import check_password_hash
from src.utils.decorators.validate_input import validate_input
from src.utils.decorators.require_auth import require_auth
from src.dto import UserCreateDTO, UserResponseDTO
from src.dto.base import ValidationError

auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

@auth_bp.route("/register")
def register_page():
    return render_template("register.html")

# vào /signin hoặc / sẽ hiển thị trang đăng nhập
@auth_bp.route("/")
@auth_bp.route("/signin")
def signin_page():
    return render_template("signin.html")

@auth_bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user_dto = UserCreateDTO(data)
        user_dto.validate()
        
        if User.query.filter_by(email=user_dto.email).first():
            return jsonify({"error": "Email đã tồn tại"}), 400

        new_user = User(
            name=user_dto.name,
            email=user_dto.email,
            password_hash=user_dto.get_password_hash()
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Đăng ký thành công"})
    
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Đăng ký thất bại"}), 500

@auth_bp.route('/api/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email và mật khẩu là bắt buộc"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Email hoặc mật khẩu không đúng"}), 400

        session['user_id'] = user.id
        
        user_response = UserResponseDTO.from_model(user)
        return jsonify({
            "message": "Đăng nhập thành công",
            "user": user_response.to_dict()
        })
    except Exception as e:
        return jsonify({"error": "Đăng nhập thất bại"}), 500

@auth_bp.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    session.clear()
    return jsonify({"message": "Đã đăng xuất"})
