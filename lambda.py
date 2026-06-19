import json
import boto3
import time

# Inisialisasi layanan AWS
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Tabel DynamoDB
table = dynamodb.Table('SurveillanceLog')

# ARN topik SNS
SNS_TOPIC_ARN = "arn:aws:sns:<region>:<account-id>:<topic-name>"


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    image_name = event['Records'][0]['s3']['object']['key']

    print(f"Memproses gambar: {image_name}")

    try:
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': image_name
                }
            },
            MaxLabels=10,
            MinConfidence=70
        )

        detected_objects = []
        is_dangerous = False
        danger_keywords = ['Weapon', 'Fire', 'Knife', 'Gun', 'Weaponry']

        for label in response['Labels']:
            object_name = label['Name']
            detected_objects.append(object_name)

            if object_name in danger_keywords:
                is_dangerous = True
                print(
                    f"Objek berbahaya terdeteksi: "
                    f"{object_name} ({label['Confidence']:.2f}%)"
                )

        status = 'CRITICAL' if is_dangerous else 'SAFE'
        timestamp = str(int(time.time()))

        table.put_item(
            Item={
                'image_id': image_name,
                'timestamp': timestamp,
                'bucket_name': bucket,
                'objects_found': detected_objects,
                'status': status
            }
        )

        print(f"Hasil analisis disimpan dengan status: {status}")

        if is_dangerous:
            message = (
                f"PERINGATAN KEAMANAN\n\n"
                f"Sistem mendeteksi objek yang berpotensi berbahaya.\n\n"
                f"Nama File        : {image_name}\n"
                f"Bucket Sumber    : {bucket}\n"
                f"Objek Terdeteksi : {', '.join(detected_objects)}\n\n"
                f"Segera lakukan pemeriksaan pada area terkait."
            )

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject="Deteksi Objek Berbahaya"
            )

            print("Notifikasi berhasil dikirim melalui Amazon SNS.")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Analisis selesai dengan status {status}')
        }

    except Exception as error:
        print(f"Terjadi kesalahan: {str(error)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Terjadi kesalahan saat memproses gambar.')
        }
