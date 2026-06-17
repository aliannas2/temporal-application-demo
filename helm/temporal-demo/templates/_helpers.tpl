{{- define "temporal-demo.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "temporal-demo.fullname" -}}
{{- .Release.Name -}}
{{- end -}}

{{- define "temporal-demo.authSecretName" -}}
{{- if .Values.auth.existingSecret -}}
{{- .Values.auth.existingSecret -}}
{{- else -}}
temporal-auth
{{- end -}}
{{- end -}}
