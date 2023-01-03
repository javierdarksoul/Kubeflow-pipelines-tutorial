from mlem.api import save
import torch
from nn import my_nn
from mlem.api import load
from abc import ABC
import io
import base64
import torch
from PIL import Image
import json
from torchvision import transforms
import numpy as np


convert_tensor = transforms.ToTensor()
#{
#  "status": "Healthy"
#}
input_type=json.loads(
    """[
        {
            "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+tbw1oNx4m8QWmkWx2yXD4LkZCADJJ+gFbviL4a63oc7COE3MW4hdn38duD976jNc9daDqllIsc9lKrMu4YGeMkdR7gj8KzcV7H8BtEvV16+1iWCeG1Wz8mOV02pIzupwCeuAp6Z98cZ90aIzLIlw0c0ZJ4KgjHoeOa+evjS9n/wnMcNxBPCYLKONFhA2FNzMpGenDcgd816V4K03wefC+m3NlpVhP+5QSXBiR5fMx825iMg5zwce3FdbOzTwgW90lu6uCm8eYrL02soIyCPQgggEdMGQ3cluiPNK0rJwrRQBNueuMkt+teNfGKxsdY8WWdxNqcNo66eieXMwVsb5DnH415Hp2rajpE5n02/urOUjBe3laMkehIPIrVm8eeLrhNknibVivoLtx/I1UPinxC3XXtUP1vJP8ay5JZJpGkldnduSzHJP41//2Q=="
        }
    ]
    """
    )

def preprocesss(instances):
    #print(instanc)
    images = []
    #instance= instances.get("instances")

    for row in instances:
        #print(data)
        image = row.get("data") or row.get("body")
        if isinstance(image, str):
            #print("holaa")
            # if the image is a string of bytesarray.
            image = base64.b64decode(image)
        if isinstance(image, (bytearray, bytes)):
            image = Image.open(io.BytesIO(image))
            image=convert_tensor(image)
                #image = self.image_processing(image)
        else:
            # if the image is a list
            image = torch.FloatTensor(image)

        images.append(image)
    #print(images)
    return torch.stack(images)

def postprocessing(x):
    print(torch.argmax(x).detach().numpy())
    return {"predictions": torch.tensor([torch.argmax(x)])}
model= my_nn()
model.load_state_dict(torch.load("weights"))

save(
    model,
    "models/my_nn",
    preprocess=preprocesss,
    postprocess=postprocessing,
    sample_data=input_type#.get("instances")
)
