import Models.Model.oauth_authorization as oauth
import Models.Model.image_to_text as image_to_text
import Models.Model.splitwise_operations as sw_ops
import json
import Models.Model.data_extraction as de

path_to_foto = 'Models/Model/image_to_text_resources/test_foto2.jpg'
access_key = oauth.save_access_key()
# receipt = image_to_text.recognise_foto(path_to_foto)

'''test receipt beginning'''
with open('training_receipt.json', 'r') as file:
    data = json.load(file)
processed_data = de.DataProcessor(data)
receipt = de.Receipt()
for item in processed_data.item_list:
    receipt.add_item(item)
receipt.set_total_price(processed_data.total_price)
'''test receipt ending'''
