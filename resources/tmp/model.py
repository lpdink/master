class ERM(Algorithm):
    """
    Empirical Risk Minimization (ERM)
    """

    def __init__(self, input_shape, num_classes, num_domains, hparams):
        super(ERM, self).__init__(input_shape, num_classes, num_domains, hparams)
        self.featurizer = networks.Featurizer(input_shape, self.hparams)
        self.classifier = nn.Linear(self.featurizer.n_outputs, num_classes)
        self.network = nn.Sequential(self.featurizer, self.classifier)
        self.optimizer = get_optimizer(
            hparams["optimizer"],
            self.network.parameters(),
            lr=self.hparams["lr"],
            weight_decay=self.hparams["weight_decay"],
        )

    def update(self, x, y, **kwargs):
        all_x = torch.cat(x)
        all_y = torch.cat(y)
        loss = F.cross_entropy(self.predict(all_x), all_y)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return {"loss": loss.item()}

    def predict(self, x):
        return self.network(x)
    
class ERMStudent(ERM):
    def __init__(self, input_shape, num_classes, num_domains, hparams):
        super().__init__(input_shape, num_classes, num_domains, hparams)
        self.distillation_loss = nn.KLDivLoss() # KL散度损失
        self.temperature = 4 # 温度4
        self.alpha = 0.25 # 蒸馏损失权重

    def update(self, x, y, teacher_pred):
        student_pred = self.predict(x)
        student_loss = F.cross_entropy(student_pred, y) # hard loss
        distillation_loss = self.distillation_loss(F.log_softmax(student_pred/self.temperature, dim=1), F.softmax(teacher_pred/self.temperature, dim=1))

        loss = (1-self.alpha)*student_loss + self.alpha*distillation_loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return {"total_loss": loss.item(), "hard_loss":student_loss.item(), "distillation_loss":distillation_loss.item()}