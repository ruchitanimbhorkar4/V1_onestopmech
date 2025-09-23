def validate_email(email):
    if '@' not in email or '.' not in email:
        return False
    if email.startswith('@') or email.endswith('@'):
        return False
    if email.startswith('.') or email.endswith('.'):
        return False
    
    if email.count('@') != 1:
        return False
        
    parts = email.split('@')
    local = parts[0]
    domain = parts[1]
    
    if not local or not domain:
        return False
        
    if '.' not in domain:
        return False
        
    return True

def validate_password(password):
    if len(password) < 8:
        return False
    
    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False
    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            has_symbol = True
    
    return has_upper and has_lower and has_digit and has_symbol

def validate_contact(contact):
    clean_contact = contact.replace(' ', '').replace('-', '')
    
    if not clean_contact.isdigit():
        return False
    
    if len(clean_contact) < 7 or len(clean_contact) > 15:
        return False
        
    return True
