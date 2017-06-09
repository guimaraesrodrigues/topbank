/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package gui;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.JSONObject;
import restful.RestServices;


/**
 *
 * @author Guilherme
 */
public class TelaLogin extends javax.swing.JFrame {

    RestServices rest;
    
    String nome;
    char[] senha;
    
    public TelaLogin(RestServices rest) {
        this.rest = rest;
        initComponents();
        this.setVisible(true);
        this.buttonLogin.requestFocus();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        labelUsuario = new javax.swing.JLabel();
        contaTextField = new javax.swing.JTextField();
        jLabel1 = new javax.swing.JLabel();
        buttonLogin = new javax.swing.JButton();
        labelUsuario4 = new javax.swing.JLabel();
        agenciaTextField = new javax.swing.JTextField();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        labelUsuario.setFont(new java.awt.Font("Tahoma", 0, 14)); // NOI18N
        labelUsuario.setText("Nº Conta:");

        contaTextField.setText("1");
        contaTextField.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                contaTextFieldActionPerformed(evt);
            }
        });

        jLabel1.setFont(new java.awt.Font("Tahoma", 1, 18)); // NOI18N
        jLabel1.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel1.setText("TopBank");
        jLabel1.setToolTipText("");

        buttonLogin.setText("ENTRAR");
        buttonLogin.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonLoginActionPerformed(evt);
            }
        });

        labelUsuario4.setFont(new java.awt.Font("Tahoma", 0, 14)); // NOI18N
        labelUsuario4.setText("Nº Agência:");

        agenciaTextField.setText("1");
        agenciaTextField.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                agenciaTextFieldActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(42, 42, 42)
                        .addComponent(jLabel1, javax.swing.GroupLayout.PREFERRED_SIZE, 220, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(buttonLogin)
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(labelUsuario)
                                    .addComponent(labelUsuario4))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                    .addComponent(contaTextField, javax.swing.GroupLayout.DEFAULT_SIZE, 173, Short.MAX_VALUE)
                                    .addComponent(agenciaTextField))))))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGap(6, 6, 6)
                .addComponent(jLabel1)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelUsuario)
                    .addComponent(contaTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelUsuario4)
                    .addComponent(agenciaTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addComponent(buttonLogin)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void contaTextFieldActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_contaTextFieldActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_contaTextFieldActionPerformed

    private void buttonLoginActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonLoginActionPerformed
       
       
        JSONObject agencia = new JSONObject();
        JSONObject conta = new JSONObject();     
          
        int n_agencia = Integer.parseInt(agenciaTextField.getText());    
        int n_conta = Integer.parseInt(contaTextField.getText());
              
        try {
            agencia = rest.getMethod(rest.getServices().getString("agencias")+n_agencia);
            conta = rest.getMethod(rest.getServices().getString("contas")+n_conta);
        } catch (IOException ex) {
            Logger.getLogger(TelaLogin.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        
        this.setVisible(false);
        TelaPrincipal tp = new TelaPrincipal(this.rest, agencia, conta);
    }//GEN-LAST:event_buttonLoginActionPerformed

    private void agenciaTextFieldActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_agenciaTextFieldActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_agenciaTextFieldActionPerformed

    /**
     * @param args the command line arguments
     */
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JTextField agenciaTextField;
    private javax.swing.JButton buttonLogin;
    private javax.swing.JTextField contaTextField;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel labelUsuario;
    private javax.swing.JLabel labelUsuario4;
    // End of variables declaration//GEN-END:variables
}
