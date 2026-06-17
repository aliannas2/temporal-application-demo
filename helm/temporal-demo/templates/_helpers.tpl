{{- define "temporal-demo.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "temporal-demo.fullname" -}}
{{- .Release.Name -}}
{{- end -}}

{{- define "temporal-demo.tlsSecretName" -}}
{{- if .Values.tls.existingSecret -}}
{{- .Values.tls.existingSecret -}}
{{- else -}}
{{- .Values.tls.secretName -}}
{{- end -}}
{{- end -}}
