import { Component } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';

@Component({
  selector: 'hackaton-speech2text-glossary-tooltip',
  templateUrl: './tooltip.component.html',
  styleUrls: ['./tooltip.component.scss'],
})
export class TooltipComponent {
  constructor(protected dialogRef: NbDialogRef<TooltipComponent>) {}

  close() {
    this.dialogRef.close();
  }
}
