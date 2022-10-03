class HyperParams:
    def __init__(self, loss_weights) -> None:
        self.loss_weights = loss_weights

def demo():
    hyperParams = HyperParams(
        [
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
        ], 
    )
    from losses import Total_loss
    total_loss = Total_loss()
    total_loss.vae.reconstruct = 1
    total_loss.vae.kld = 2
    total_loss.vrnn.predict.z = 3
    total_loss.vrnn.predict.image = 4
    total_loss.vrnn.kld = 5
    total_loss.weight_decay = 6
    print(total_loss.sum(hyperParams.loss_weights))

if __name__ == '__main__':
    demo()
