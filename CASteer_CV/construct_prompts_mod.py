import random

def get_imagenet_classes():
    imagenet_classes = []
    
    # Make sure 'imagenet_classes.txt' is in the same folder
    try:
        f = open('imagenet_classes.txt', 'r')
        for line in f.readlines():
            imagenet_classes.append(line.strip())
        f.close()
    except FileNotFoundError:
        print("Warning: imagenet_classes.txt not found.")
        return []
    
    return imagenet_classes

def get_prompts_concrete(num=50, concept_pos='Snoopy', concept_neg=None):
    
    imagenet_classes = get_imagenet_classes()
    
    # 1. Slice the list to get only indices 400 to 914 (inclusive)
    # Python slicing is [start:end], where 'end' is exclusive, so we use 915.
    subset_classes = imagenet_classes[400:915]
    
    # 2. Randomly pick 'num' classes from this subset
    sample_size = min(num, len(subset_classes))
    selected_classes = random.sample(subset_classes, sample_size)
    
    prompts_pos = []
    prompts_neg = []
    for cls in selected_classes:
        prompts_pos.append(cls+' with {}'.format(concept_pos))
        if concept_neg is not None:
            prompts_neg.append(cls+' with {}'.format(concept_neg))
        else:
            prompts_neg.append(cls)
            
    return prompts_pos, prompts_neg

def get_prompts_style(num=50, concept_pos='anime', concept_neg=None):
    
    imagenet_classes = get_imagenet_classes()
    
    # 1. Slice the list to get only indices 400 to 914 (inclusive)
    subset_classes = imagenet_classes[400:915]
    
    # 2. Randomly pick 'num' classes from this subset
    sample_size = min(num, len(subset_classes))
    selected_classes = random.sample(subset_classes, sample_size)
    
    prompts_pos = []
    prompts_neg = []
    for cls in selected_classes:
        prompts_pos.append(cls+', {} style'.format(concept_pos))
        if concept_neg is not None:
            prompts_neg.append(cls+', {} style'.format(concept_neg))
        else:
            prompts_neg.append(cls)
        
    return prompts_pos, prompts_neg

def get_prompts_human_related(concept_pos='nudity', concept_neg=None):
    B = ['a girl', 'two men', 'a man', 'a woman', 'an old man', 'a boy', 'boys', 'group of people']
    C = ['on a beach', 'zoomed in', 'talking', 'dancing on the street', 'playing guitar', 'enjoying nature', \
         'smiling', 'in futuristic spaceship', 'with kittens', 'in a strange pose', 'realism', 'colorful background', '']
    
    prompts_pos = []
    prompts_neg = []
    for b in B:
        for c in C:
            prompts_pos.append(b+' '+c+', {}'.format(concept_pos))
            if concept_neg is not None:
                prompts_neg.append(b+' '+c+', {}'.format(concept_neg))
            else:
                prompts_neg.append(b+' '+c)
        
            
    return prompts_pos, prompts_neg