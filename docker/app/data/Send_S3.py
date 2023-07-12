import boto3
from io import BytesIO
from PIL import Image 

def send_s3(image, filename):
    
    session = boto3.Session(
    aws_access_key_id='AKIA34NLK2O6SQVDN4GL',
    aws_secret_access_key='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',
    region_name='ap-northeast-2'
    ) 
    
# S3 클라이언트 생성
    s3 = session.client('s3')

# 업로드할 파일 경로 및 버킷 이름 지정
    key = f'images/{filename}.jpg'
    bucket_name = 'ddcctv-images'

    # 이미지 객체를 저장할 때
    buffered =  BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    
    response = s3.put_object(
    Body=img_bytes,
    Bucket=bucket_name,
    Key=key
    )
    
    #파일로 저장할 때
    # image = Image.open(imagefile)
    # buffered = BytesIO()
    # image.save(buffered, format='JPEG')
    # img_bytes = buffered.getvalue()
    
    # response = s3.put_object(
    # Body=img_bytes,
    # Bucket=bucket_name,
    # Key=key
    # )
    
if __name__ == "__main__":
    send_s3('images/2023_04_12_191946.jpg', '1234')
    
