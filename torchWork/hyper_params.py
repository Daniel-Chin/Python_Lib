from typing import List

class BaseHyperParams:
    def __init__(self) -> None:
        self.loss_weights_tree: List = None

def demo():
    import torch
    import torch.nn.functional as F

    class HyperParams(BaseHyperParams):
        def __init__(self):
            super().__init__()
            self.rnn_width = None
            self.do_grad_clip = None
            self.grad_clip_ceil = None
            self.image_loss = None
        
        def validate(self):
            if self.do_grad_clip:
                assert self.grad_clip_ceil > 0
            else:
                assert self.grad_clip_ceil is None
        
        def expand(self):
            self.imgCriterion = {
                'bce': torch.nn.BCELoss(), 
                'mse': F.mse_loss, 
            }[self.image_loss]

    hyperParams = HyperParams()
    hyperParams.loss_weights_tree=[
        ('vae', .5, [
            ('reconstruct', .9, None), 
            ('kld', .1, None), 
        ]), 
        ('vrnn', .4, [
            ('predict', .9, [
                ('z', .5, None),
                ('image', .5, None),
            ]), 
            ('kld', .1, None), 
        ]), 
        ('weight_decay', .1, None), 
    ]
    hyperParams.rnn_width = 8
    hyperParams.do_grad_clip = True
    hyperParams.grad_clip_ceil = 1
    hyperParams.image_loss = 'mse'
    hyperParams.validate()
    hyperParams.expand()

    from losses import Total_loss
    total_loss = Total_loss()
    total_loss.vae.reconstruct = 1
    total_loss.vae.kld = 2
    total_loss.vrnn.predict.z = 3
    total_loss.vrnn.predict.image = 4
    total_loss.vrnn.kld = 5
    total_loss.weight_decay = 6
    print(total_loss.sum(hyperParams.loss_weights_tree))

if __name__ == '__main__':
    demo()
