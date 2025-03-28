from app.core.models.db_model import Measures, ParameterType, TypeAlert


class ValidationAlert:
    @staticmethod
    def validate_alert(
        measure: Measures, parameter_type: ParameterType, type_alert: TypeAlert
    ) -> bool:
        """
        Valida se uma medida gera um alerta com base no tipo do parâmetro
        e no tipo de alerta.

        Args:
            measure (Measures): A medida registrada.
            parameter_type (ParameterType): O tipo do parâmetro associado à medida.
            type_alert (TypeAlert): O tipo de alerta a ser validado.

        Returns:
            bool: True se a medida gerar um alerta, False caso contrário.
        """
        # Ajustar o valor da medida com base no fator e offset do tipo de parâmetro
        try:
            adjusted_value = (float(measure.value) * (parameter_type.factor or 1)) + (
                parameter_type.offset or 0
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Erro ao ajustar o valor da medida: {e}")

        # Validar o valor ajustado com base no operador matemático do tipo de alerta
        if type_alert.math_signal == ">":
            return adjusted_value > type_alert.value
        if type_alert.math_signal == ">=":
            return adjusted_value >= type_alert.value
        if type_alert.math_signal == "<":
            return adjusted_value < type_alert.value
        if type_alert.math_signal == "<=":
            return adjusted_value <= type_alert.value
        if type_alert.math_signal == "==":
            return adjusted_value == type_alert.value
        if type_alert.math_signal == "!=":
            return adjusted_value != type_alert.value
        raise ValueError(f"Operador matemático inválido: {type_alert.math_signal}")
